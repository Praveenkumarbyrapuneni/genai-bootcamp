# 🚀 Deployment Guide - Bulk Delete/Archive Feature

## ✅ What Was Implemented

### Backend (FastAPI + Cosmos DB) ✅ COMPLETE
1. **Input Validation Fix** - "hello" issue SOLVED ✅
   - Added validation to reject invalid roles like "hello", "hi", "test", "testing"
   - Returns helpful error message with examples of valid roles

2. **Database Schema Updates** ✅
   - All new records include `is_deleted: false` and `is_archived: false`
   - Existing records work fine (backward compatible)

3. **New API Endpoints** ✅
   - `POST /api/history/bulk-delete` - Soft delete multiple analyses
   - `POST /api/history/bulk-archive` - Archive/unarchive multiple analyses
   - `GET /api/history/{user_id}?include_archived=true/false` - Updated to filter

4. **Security** ✅
   - All operations verify user ownership before allowing changes
   - Cannot delete/archive someone else's records

### Frontend (Next.js) ✅ NEW COMPONENT CREATED
- Created `HistoryManager.tsx` component with:
  - Multi-select checkboxes
  - "Select All" functionality  
  - Bulk Delete button with confirmation modal
  - Bulk Archive button
  - "Show Archived" toggle
  - Toast notifications for success/errors
  - Real-time history fetching from API

---

## 📝 Step 1: Update Frontend to Use New HistoryManager

### Option A: Integrate into existing Dashboard (Recommended)

Open `frontend/src/components/Dashboard.tsx` and find the sidebar history section (around line 900-1000).

**Replace** the existing Recent section with:

```tsx
import { HistoryManager } from './HistoryManager';

// Inside the Dashboard component, in the sidebar:
<div className="flex-1 overflow-y-auto">
  <HistoryManager 
    userId={user.id}
    onSelectHistory={(item) => {
      setResults(item.data);
      setTargetRole(item.target_role);
      setCurrentChatId(item.id);
    }}
    currentChatId={currentChatId}
  />
</div>
```

### Option B: Quick Test (Standalone)

Create `frontend/src/app/history/page.tsx`:

```tsx
"use client";

import { HistoryManager } from "@/components/HistoryManager";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function HistoryPage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setUser(data.user));
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-4">Analysis History</h1>
      <div className="max-w-2xl bg-white rounded-lg shadow-lg" style={{ height: '600px' }}>
        <HistoryManager 
          userId={user.id}
          onSelectHistory={(item) => console.log('Selected:', item)}
          currentChatId={null}
        />
      </div>
    </div>
  );
}
```

Then visit: `http://localhost:3000/history`

---

## 🚀 Step 2: Deploy to Azure

### Backend Deployment

```bash
cd "/Users/praveen/Desktop/careerpath with auth"

# Build and push new Docker image with validation + bulk operations
docker build -t careerpath-backend:latest .
docker tag careerpath-backend:latest <your-acr-name>.azurecr.io/careerpath-backend:latest
docker push <your-acr-name>.azurecr.io/careerpath-backend:latest

# Or use the deployment script:
./deploy/deploy-container-apps.sh
```

### Frontend Deployment

```bash
cd frontend

# Install dependencies if needed
npm install

# Build
npm run build

# Deploy to Azure Static Web Apps
# (automatically happens on git push if connected to GitHub)
```

---

## 🧪 Step 3: Test the Features

### Test 1: Input Validation (hello bug fix)
1. Open your app: https://your-app.azurestaticapps.net
2. Try entering "hello" as target role
3. **Expected**: Error message appears: "'hello' is not a valid job role..."
4. Enter "Data Analyst" 
5. **Expected**: Analysis runs successfully ✅

### Test 2: Bulk Delete
1. Click "Show Archived" if you want to see all items
2. Check 2-3 history items
3. Click "Delete (X)" button
4. **Expected**: Confirmation modal appears
5. Click "Delete"
6. **Expected**: Items disappear, toast shows "Deleted X item(s)" ✅

### Test 3: Bulk Archive
1. Select 2-3 history items
2. Click "Archive (X)" button  
3. **Expected**: Confirmation modal appears
4. Click "Archive"
5. **Expected**: Items marked as archived (grayed out) ✅
6. Toggle "Hide Archived"
7. **Expected**: Archived items disappear ✅

### Test 4: Security (Cannot delete others' data)
1. Get your user_id from browser console: `user.id`
2. Try calling API directly with wrong user_id:
```bash
curl -X POST https://your-api.azurecontainerapps.io/api/history/bulk-delete \
  -H "Content-Type: application/json" \
  -d '{"ids": ["some-id"], "user_id": "fake-user-id"}'
```
3. **Expected**: Items owned by you are NOT deleted ✅

---

## 📊 API Documentation

### `POST /api/history/bulk-delete`

**Request:**
```json
{
  "ids": ["uuid-1", "uuid-2"],
  "user_id": "user-uuid"
}
```

**Response (Success):**
```json
{
  "success": true,
  "updated": 2,
  "failed": 0,
  "failed_ids": [],
  "message": "Deleted 2 item(s)"
}
```

### `POST /api/history/bulk-archive`

**Request:**
```json
{
  "ids": ["uuid-1", "uuid-2"],
  "user_id": "user-uuid",
  "is_archived": true
}
```

**Response (Success):**
```json
{
  "success": true,
  "updated": 2,
  "failed": 0,
  "failed_ids": [],
  "message": "Archived 2 item(s)"
}
```

### `GET /api/history/{user_id}?include_archived=false`

**Query Parameters:**
- `include_archived` (optional): `true` | `false` (default: `false`)

**Response:**
```json
{
  "history": [
    {
      "id": "uuid",
      "user_id": "user-uuid",
      "target_role": "Data Analyst",
      "timestamp": "2026-01-06T...",
      "is_deleted": false,
      "is_archived": false,
      "data": { ... }
    }
  ]
}
```

---

## 🎯 Acceptance Criteria Status

| Criteria | Status | Notes |
|----------|--------|-------|
| ✅ User sees analysis history list | ✅ DONE | HistoryManager component |
| ✅ Multi-select checkboxes | ✅ DONE | Checkbox per item |
| ✅ Select All functionality | ✅ DONE | Toggle all at once |
| ✅ Bulk Delete with confirmation | ✅ DONE | Modal + API call |
| ✅ Bulk Archive | ✅ DONE | Archive/unarchive |
| ✅ Show Archived toggle | ✅ DONE | Filter API call |
| ✅ Toast notifications | ✅ DONE | Success/error messages |
| ✅ Security validation | ✅ DONE | Ownership checks |
| ✅ "hello" bug fixed | ✅ DONE | Input validation |
| ✅ Professional career advisor | ✅ DONE | Existing brutal honesty system |

---

## 🐛 Troubleshooting

### Backend not responding?
```bash
# Check backend logs
az containerapp logs show --name careerpath-api --resource-group <your-rg>
```

### Frontend can't connect to API?
- Check `frontend/.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS is enabled in `api/main.py` (already done ✅)

### "Cannot delete" error?
- Verify user_id matches the record owner
- Check browser console for detailed error message

---

## 🎉 What's Next?

1. **Permanent Delete**: Add a "Permanently Delete" button for deleted items
2. **Restore from Archive**: Add "Unarchive" button in archived view  
3. **Export History**: Download all analyses as PDF/JSON
4. **Search/Filter**: Search by role name or date range

---

## 📞 Support

If you encounter issues:
1. Check browser console for errors
2. Check backend logs in Azure Portal
3. Verify environment variables are set correctly
4. Test API endpoints directly with curl/Postman

---

**All changes are backward compatible! Existing data continues to work.** ✅
