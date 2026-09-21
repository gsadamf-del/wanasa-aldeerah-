#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
flutter create --platforms=android,ios --org com.wanasa --project-name wanasa_aldeerah .
flutter pub get
printf '\nPlatform projects generated. Add Firebase config files before device builds.\n'
