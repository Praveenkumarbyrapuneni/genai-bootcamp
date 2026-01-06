// src/components/HistoryManager.tsx
"use client";

import { useState, useEffect } from "react";

interface HistoryItem {
  id: string;
  target_role: string;
  timestamp: string;
  data?: any;
  is_archived?: boolean;
}

interface HistoryManagerProps {
  userId: string;
  onSelectHistory: (item: HistoryItem) => void;
  currentChatId: string | null;
}

export function HistoryManager({ userId, onSelectHistory, currentChatId }: HistoryManagerProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [showArchived, setShowArchived] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  const [confirmAction, setConfirmAction] = useState<{ type: 'delete' | 'archive', ids: string[] } | null>(null);

  // Fetch history from API
  const fetchHistory = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/history/${userId}?include_archived=${showArchived}`
      );
      if (response.ok) {
        const data = await response.json();
        setHistory(data.history || []);
      }
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  useEffect(() => {
    if (userId) {
      fetchHistory();
    }
  }, [userId, showArchived]);

  // Toggle selection
  const toggleSelect = (id: string) => {
    const newSelection = new Set(selectedIds);
    if (newSelection.has(id)) {
      newSelection.delete(id);
    } else {
      newSelection.add(id);
    }
    setSelectedIds(newSelection);
  };

  // Select all
  const selectAll = () => {
    if (selectedIds.size === history.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(history.map(h => h.id)));
    }
  };

  // Bulk delete
  const handleBulkDelete = async () => {
    if (selectedIds.size === 0) return;

    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/history/bulk-delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ids: Array.from(selectedIds),
          user_id: userId
        })
      });

      const result = await response.json();
      if (response.ok) {
        setToast({ message: result.message || `Deleted ${result.updated} item(s)`, type: 'success' });
        setSelectedIds(new Set());
        await fetchHistory();
      } else {
        setToast({ message: result.detail || 'Delete failed', type: 'error' });
      }
    } catch (error) {
      setToast({ message: 'Network error during delete', type: 'error' });
    } finally {
      setLoading(false);
      setConfirmAction(null);
    }
  };

  // Bulk archive/unarchive
  const handleBulkArchive = async (archive: boolean) => {
    if (selectedIds.size === 0) return;

    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/history/bulk-archive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ids: Array.from(selectedIds),
          user_id: userId,
          is_archived: archive
        })
      });

      const result = await response.json();
      if (response.ok) {
        const action = archive ? 'Archived' : 'Unarchived';
        setToast({ message: result.message || `${action} ${result.updated} item(s)`, type: 'success' });
        setSelectedIds(new Set());
        await fetchHistory();
      } else {
        setToast({ message: result.detail || 'Archive operation failed', type: 'error' });
      }
    } catch (error) {
      setToast({ message: 'Network error during archive', type: 'error' });
    } finally {
      setLoading(false);
      setConfirmAction(null);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 ${
          toast.type === 'success' ? 'bg-green-500' : 
          toast.type === 'error' ? 'bg-red-500' : 'bg-blue-500'
        } text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3`}>
          <span>{toast.message}</span>
          <button onClick={() => setToast(null)} className="ml-2 hover:opacity-80">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Confirmation Modal */}
      {confirmAction && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {confirmAction.type === 'delete' ? 'Delete Analyses?' : 'Archive Analyses?'}
            </h3>
            <p className="text-gray-600 mb-6">
              {confirmAction.type === 'delete' 
                ? `Are you sure you want to delete ${confirmAction.ids.length} item(s)? This action cannot be undone.`
                : `Archive ${confirmAction.ids.length} item(s)?`
              }
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setConfirmAction(null)}
                className="flex-1 px-4 py-2.5 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (confirmAction.type === 'delete') {
                    handleBulkDelete();
                  } else {
                    handleBulkArchive(true);
                  }
                }}
                className={`flex-1 px-4 py-2.5 rounded-xl font-medium text-white ${
                  confirmAction.type === 'delete' 
                    ? 'bg-red-600 hover:bg-red-700' 
                    : 'bg-yellow-600 hover:bg-yellow-700'
                }`}
              >
                {confirmAction.type === 'delete' ? 'Delete' : 'Archive'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header with Actions */}
      <div className="p-3 border-b border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xs font-semibold text-gray-700">History</h3>
          <button
            onClick={() => setShowArchived(!showArchived)}
            className="text-xs text-indigo-600 hover:text-indigo-700"
          >
            {showArchived ? 'Hide Archived' : 'Show Archived'}
          </button>
        </div>

        {/* Bulk Actions */}
        {selectedIds.size > 0 && (
          <div className="flex items-center gap-2 mt-2">
            <button
              onClick={() => setConfirmAction({ type: 'delete', ids: Array.from(selectedIds) })}
              disabled={loading}
              className="flex-1 px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-xs font-medium hover:bg-red-200 disabled:opacity-50"
            >
              Delete ({selectedIds.size})
            </button>
            <button
              onClick={() => setConfirmAction({ type: 'archive', ids: Array.from(selectedIds) })}
              disabled={loading}
              className="flex-1 px-3 py-1.5 bg-yellow-100 text-yellow-700 rounded-lg text-xs font-medium hover:bg-yellow-200 disabled:opacity-50"
            >
              Archive ({selectedIds.size})
            </button>
          </div>
        )}
      </div>

      {/* Select All Checkbox */}
      {history.length > 0 && (
        <div className="px-3 py-2 border-b border-gray-200">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={selectedIds.size === history.length && history.length > 0}
              onChange={selectAll}
              className="w-4 h-4 text-indigo-600 rounded"
            />
            <span className="text-xs text-gray-600">Select All</span>
          </label>
        </div>
      )}

      {/* History List */}
      <div className="flex-1 overflow-y-auto px-3 py-2">
        {history.length === 0 ? (
          <p className="text-xs text-gray-400 px-3 py-2">No history found</p>
        ) : (
          <div className="space-y-1">
            {history.map((item) => (
              <div
                key={item.id}
                className={`group relative flex items-center gap-2 p-2 rounded-lg transition-all ${
                  currentChatId === item.id 
                    ? 'bg-indigo-100' 
                    : 'hover:bg-gray-100'
                } ${item.is_archived ? 'opacity-60' : ''}`}
              >
                <input
                  type="checkbox"
                  checked={selectedIds.has(item.id)}
                  onChange={() => toggleSelect(item.id)}
                  className="w-4 h-4 text-indigo-600 rounded"
                  onClick={(e) => e.stopPropagation()}
                />
                <button
                  onClick={() => onSelectHistory(item)}
                  className="flex-1 text-left text-sm text-gray-700 truncate"
                >
                  {item.target_role}
                  {item.is_archived && <span className="ml-2 text-xs text-gray-400">(archived)</span>}
                </button>
                <span className="text-xs text-gray-400">
                  {new Date(item.timestamp).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
