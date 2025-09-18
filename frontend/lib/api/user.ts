import { apiClient } from './client';

export async function exportUserData() {
  const response = await apiClient.get('/user/export-data', {
    responseType: 'blob',
  });
  
  // Create download
  const blob = new Blob([response.data], { type: 'application/json' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `export-${Date.now()}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export async function deleteAccount() {
  const response = await apiClient.delete('/user/delete-account');
  return response.data;
}