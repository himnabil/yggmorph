use clap::{Parser, Subcommand};
use std::fs;
use std::io;
use std::path::{PathBuf};

#[derive(Parser)]
#[command(name = "yggmorph", about = "Manage Maven settings.xml profiles")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Maven {
        #[command(subcommand)]
        command: MavenCommand,
    },
}

#[derive(Subcommand)]
enum MavenCommand {
    Apply {
        #[arg(short, long)]
        profile: String,
    },
    Save {
        #[arg(short, long)]
        profile: String,
    },
    #[command(name = "list-profiles")]
    ListProfiles,
}

fn home_dir() -> PathBuf {
    std::env::var("HOME").map(PathBuf::from).expect("HOME env not set")
}

fn m2_dir() -> PathBuf {
    home_dir().join(".m2")
}

fn settings_xml() -> PathBuf {
    m2_dir().join("settings.xml")
}

fn ygg_dir() -> PathBuf {
    home_dir().join(".yggmorph")
}

fn ygg_maven_dir() -> PathBuf {
    ygg_dir().join("maven")
}

fn ensure_dirs() -> io::Result<()> {
    fs::create_dir_all(ygg_maven_dir())
}

fn maven_remove_settings() -> io::Result<()> {
    let path = settings_xml();
    if path.exists() {
        fs::remove_file(&path)?;
        println!("settings.xml removed from .m2");
    } else {
        println!("No settings.xml found to remove");
    }
    Ok(())
}

fn maven_apply_profile(profile: &str) -> io::Result<()> {
    let src = ygg_maven_dir().join(format!("settings.{profile}.xml"));
    if src.exists() {
        fs::copy(&src, settings_xml())?;
        println!("Profile '{profile}' applied.");
    } else {
        println!("Profile '{profile}' not found in .yggmorph");
    }
    Ok(())
}

fn maven_save_current_profile(profile: &str) -> io::Result<()> {
    let src = settings_xml();
    if src.exists() {
        let dst = ygg_maven_dir().join(format!("settings.{profile}.xml"));
        fs::copy(&src, dst)?;
        println!("Current settings.xml saved as profile '{profile}' in .yggmorph");
    } else {
        println!("No settings.xml found in .m2 to save.");
    }
    Ok(())
}

fn maven_list_profiles() {
    let dir = ygg_maven_dir();
    let mut profiles = Vec::new();
    if let Ok(entries) = fs::read_dir(&dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                if let Some(stripped) = name.strip_prefix("settings.") {
                    if let Some(stripped) = stripped.strip_suffix(".xml") {
                        profiles.push(stripped.to_string());
                    }
                }
            }
        }
    }
    if profiles.is_empty() {
        println!("No profiles found in .yggmorph");
    } else {
        profiles.sort();
        println!("Available profiles:");
        for profile in profiles {
            println!(" - {profile}");
        }
    }
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();
    ensure_dirs()?;
    match cli.command {
        Commands::Maven { command } => match command {
            MavenCommand::Apply { profile } => {
                if profile == "default" {
                    maven_remove_settings()?;
                } else {
                    maven_apply_profile(&profile)?;
                }
            }
            MavenCommand::Save { profile } => maven_save_current_profile(&profile)?,
            MavenCommand::ListProfiles => maven_list_profiles(),
        },
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use serial_test::serial;
    use tempfile::tempdir;

    #[test]
    #[serial]
    fn home_and_m2_dirs_use_home_env() {
        let tmp = tempdir().unwrap();
        unsafe { std::env::set_var("HOME", tmp.path()); }
        assert_eq!(home_dir(), tmp.path());
        assert_eq!(m2_dir(), tmp.path().join(".m2"));
    }

    #[test]
    #[serial]
    fn ensure_dirs_creates_structure() {
        let tmp = tempdir().unwrap();
        unsafe { std::env::set_var("HOME", tmp.path()); }
        ensure_dirs().unwrap();
        assert!(tmp.path().join(".yggmorph/maven").exists());
    }

    #[test]
    #[serial]
    fn save_and_apply_roundtrip() {
        let tmp = tempdir().unwrap();
        unsafe { std::env::set_var("HOME", tmp.path()); }
        let m2 = tmp.path().join(".m2");
        std::fs::create_dir_all(&m2).unwrap();
        std::fs::write(m2.join("settings.xml"), "<settings>").unwrap();

        ensure_dirs().unwrap();
        maven_save_current_profile("foo").unwrap();

        std::fs::remove_file(m2.join("settings.xml")).unwrap();
        maven_apply_profile("foo").unwrap();
        assert!(m2.join("settings.xml").exists());
    }
}

