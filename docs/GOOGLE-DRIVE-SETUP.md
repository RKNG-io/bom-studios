# Google Drive Setup Guide

This guide walks you through setting up Google Drive integration for BOM Studios video delivery.

**Account:** jeroen.bomstudios@gmail.com

---

## Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Sign in with **jeroen.bomstudios@gmail.com**
3. Click "Select a project" → "New Project"
4. Name it: `BOM Studios`
5. Click "Create"

---

## Step 2: Enable Google Drive API

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Drive API"
3. Click on it and click **Enable**

---

## Step 3: Create Service Account

A Service Account lets the API upload files without user interaction.

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in:
   - Service account name: `bom-studios-api`
   - Service account ID: `bom-studios-api` (auto-filled)
   - Description: `BOM Studios video delivery`
4. Click **Create and Continue**
5. Skip the optional permissions, click **Done**

---

## Step 4: Download Credentials

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON** format
5. Click **Create**
6. A JSON file will download — **keep this safe!**

---

## Step 5: Create Shared Folder in Google Drive

1. Go to https://drive.google.com (signed in as jeroen.bomstudios@gmail.com)
2. Click **New** → **Folder**
3. Name it: `BOM Studios Videos`
4. Right-click the folder → **Share**
5. Add the service account email (looks like `bom-studios-api@bom-studios-xxxxx.iam.gserviceaccount.com`)
6. Give it **Editor** access
7. Click **Share**

---

## Step 6: Get Folder ID

1. Open the `BOM Studios Videos` folder in Drive
2. Look at the URL: `https://drive.google.com/drive/folders/XXXXXXXXX`
3. Copy the folder ID (the `XXXXXXXXX` part)

---

## Step 7: Configure Environment Variables

### For DigitalOcean (Production)

1. Go to https://cloud.digitalocean.com/apps
2. Open **bom-studios-api**
3. Go to **Settings** → **App-Level Environment Variables**
4. Add:

```
GOOGLE_SERVICE_ACCOUNT_JSON=<paste entire contents of the JSON file>
GOOGLE_DRIVE_FOLDER_ID=<folder ID from step 6>
```

**Important:** The JSON must be on one line. You can use this command to format it:

```bash
cat your-downloaded-file.json | tr -d '\n' | pbcopy
```

### For Local Development

Create/update `/api/.env`:

```bash
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
```

And place the downloaded JSON file as `/api/google-credentials.json`

---

## Step 8: Test the Integration

Once configured, test with:

```bash
# Check API health
curl https://bom-studios-api.ondigitalocean.app/health

# The deliver endpoint will be available at:
# POST /api/videos/{video_id}/deliver
```

---

## How It Works

When a video is approved and you click "Deliver":

1. API creates a client folder in Google Drive (e.g., `BOM Studios Videos/Client Name/`)
2. Video is uploaded to that folder
3. Folder is shared with the client's email (view access)
4. Video status changes to "delivered"
5. Client receives the Drive link

---

## Folder Structure

```
BOM Studios Videos/
├── Client A/
│   ├── video-001.mp4
│   └── video-002.mp4
├── Client B/
│   └── video-003.mp4
└── Client C/
    └── ...
```

---

## Troubleshooting

### "Google Drive not configured"
- Check that `GOOGLE_SERVICE_ACCOUNT_JSON` or `google-credentials.json` exists
- Verify the JSON is valid (no extra characters)

### "Permission denied"
- Make sure the service account has Editor access to the Drive folder
- Check the folder ID is correct

### Videos not appearing in Drive
- Verify the service account email has access to the folder
- Check API logs in DigitalOcean for errors

---

## Security Notes

- The service account JSON contains private keys — never commit it to git
- The `.gitignore` already excludes `google-credentials.json`
- In production, use environment variables only
- Clients only get **view** access to their videos
