#!/bin/bash

# --- 1. SET ENVIRONMENT VARIABLES (SAFETY CHECK) ---
# Memastikan variabel SECRET_KEY tersedia.
# Railway seharusnya sudah menyediakannya, tapi ini adalah praktik yang baik.
if [ -z "$SECRET_KEY" ]; then
    echo "ERROR: SECRET_KEY is not set. Aborting build."
    exit 1
fi

# --- 2. INSTALL DEPENDENCIES ---
echo "Installing dependencies from requirements.txt..."
# Menggunakan --no-cache-dir untuk menghemat ruang disk di lingkungan deployment
pip install --no-cache-dir -r requirements.txt

# --- 3. DATABASE MIGRATION ---
echo "Running database migrations..."
# Memastikan database (Supabase) sudah siap dan skema terbaru
python manage.py migrate --noinput

# --- 4. COLLECT STATIC FILES ---
echo "Collecting static files (admin CSS/JS)..."
# Mengumpulkan semua file statis ke dalam STATIC_ROOT (akan digunakan oleh Whitenoise)
python manage.py collectstatic --noinput

echo "Build script finished successfully."