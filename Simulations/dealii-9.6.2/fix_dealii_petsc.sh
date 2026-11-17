#!/bin/bash

# === Set correct PETSC and SLEPC paths ===
PETSC_PATH="$HOME/miniconda3/lib/python3.13/site-packages/petsc"
SLEPC_PATH="$HOME/miniconda3/lib/python3.13/site-packages/slepc"
SRC_DIR="$HOME/Downloads/dealii-9.6.2"
BUILD_DIR="$SRC_DIR/build"

echo "🔍 Searching for broken PETSC_DIR references..."
grep -r '\$$HOME/miniconda3/lib/python3.13/site-packages/petsc' "$SRC_DIR"

echo "🩹 Patching any bad CMake files..."
find "$SRC_DIR" -type f -name "*.cmake" -o -name "CMakeLists.txt" | while read -r file; do
  sed -i "s|\\\$\\\$HOME/miniconda3/lib/python3.13/site-packages/petsc|${PETSC_PATH}|g" "$file"
done

echo "🧼 Cleaning previous build..."
rm -rf "$BUILD_DIR/CMakeCache.txt" "$BUILD_DIR/CMakeFiles" "$BUILD_DIR/compile_commands.json"

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR" || exit 1

echo "⚙️ Re-running CMake configuration..."
cmake -DCMAKE_BUILD_TYPE=Release \
  -DDEAL_II_WITH_PETSC=ON \
  -DPETSC_DIR="${PETSC_PATH}" \
  -DDEAL_II_WITH_SLEPC=ON \
  -DSLEPC_DIR="${SLEPC_PATH}" \
  -DDEAL_II_WITH_MPI=ON \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  ..

echo "✅ CMake finished. Verifying no \$\$HOME/miniconda3/lib/python3.13/site-packages/petsc remains in build..."
if grep -q '\$$HOME/miniconda3/lib/python3.13/site-packages/petsc' compile_commands.json; then
  echo "❌ ERROR: Broken PETSC_DIR still present."
else
  echo "✅ FIXED: No broken PETSC_DIR detected. You can now build."
  echo "👉 Run: make -j$(nproc)"
fi

