use assert_cmd::prelude::*;
use serial_test::serial;
use std::process::Command;
use tempfile::tempdir;

#[test]
#[serial]
fn save_and_apply_via_cli() {
    let tmp = tempdir().unwrap();
    unsafe { std::env::set_var("HOME", tmp.path()); }

    // create initial settings.xml
    std::fs::create_dir_all(tmp.path().join(".m2")).unwrap();
    std::fs::write(tmp.path().join(".m2/settings.xml"), "<settings>").unwrap();

    Command::cargo_bin("yggmorph")
        .unwrap()
        .args(["maven", "save", "-p", "foo"])
        .assert()
        .success();

    std::fs::remove_file(tmp.path().join(".m2/settings.xml")).unwrap();

    Command::cargo_bin("yggmorph")
        .unwrap()
        .args(["maven", "apply", "-p", "foo"])
        .assert()
        .success();

    assert!(tmp.path().join(".m2/settings.xml").exists());
}

#[test]
#[serial]
fn apply_default_removes_settings() {
    let tmp = tempdir().unwrap();
    unsafe { std::env::set_var("HOME", tmp.path()); }
    std::fs::create_dir_all(tmp.path().join(".m2")).unwrap();
    std::fs::write(tmp.path().join(".m2/settings.xml"), "<settings>").unwrap();

    Command::cargo_bin("yggmorph")
        .unwrap()
        .args(["maven", "apply", "-p", "default"])
        .assert()
        .success();

    assert!(!tmp.path().join(".m2/settings.xml").exists());
}
