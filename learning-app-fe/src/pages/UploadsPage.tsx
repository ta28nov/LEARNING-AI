import React, { useCallback, useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Trash2, RefreshCw, Download, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useUploadStore } from '@/stores/uploadStore';
import { formatFileSize, formatRelativeTime } from '@/lib/utils';
import toast from 'react-hot-toast';

export function UploadsPage() {
  const { 
    uploads, 
    fetchUploads, 
    uploadFile, 
    deleteUpload, 
    reprocessUpload, 
    isUploading, 
    uploadProgress 
  } = useUploadStore();
  
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    fetchUploads();
  }, [fetchUploads]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      try {
        await uploadFile(file);
      } catch (error) {
        console.error('Failed to upload file:', error);
      }
    }
  }, [uploadFile]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true,
  });

  const handleDelete = async (uploadId: string) => {
    if (confirm('Are you sure you want to delete this file?')) {
      try {
        await deleteUpload(uploadId);
      } catch (error) {
        console.error('Failed to delete upload:', error);
      }
    }
  };

  const handleReprocess = async (uploadId: string) => {
    try {
      await reprocessUpload(uploadId);
      toast.success('File reprocessing started');
    } catch (error) {
      console.error('Failed to reprocess upload:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'processing':
        return <Clock className="h-5 w-5 text-yellow-600" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-600" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'processing':
        return 'text-yellow-600 bg-yellow-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">File Uploads</h1>
        <p className="text-gray-600">Upload and manage your learning documents</p>
      </div>

      {/* Upload Zone */}
      <Card>
        <CardContent className="p-8">
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-2xl p-12 text-center transition-colors cursor-pointer
              ${isDragActive || dragActive 
                ? 'border-primary-500 bg-primary-50' 
                : 'border-gray-300 hover:border-gray-400'
              }
            `}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              <div className="mx-auto h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center">
                <Upload className="h-8 w-8 text-primary-600" />
              </div>
              
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {isDragActive ? 'Drop files here' : 'Upload your files'}
                </h3>
                <p className="text-gray-600 mt-2">
                  Drag and drop files here, or click to select files
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Supports PDF, DOCX, and TXT files (max 10MB each)
                </p>
              </div>
              
              {!isDragActive && (
                <Button>
                  Choose Files
                </Button>
              )}
            </div>
          </div>

          {/* Upload Progress */}
          {isUploading && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3 mb-2">
                <LoadingSpinner size="sm" />
                <span className="text-sm font-medium text-blue-900">Uploading...</span>
              </div>
              <Progress value={uploadProgress} className="w-full" />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Files Table */}
      <Card>
        <CardHeader>
          <CardTitle>Your Files</CardTitle>
          <CardDescription>
            {uploads.length} file{uploads.length !== 1 ? 's' : ''} uploaded
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {uploads.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-900">File Name</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Size</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Date Added</th>
                    <th className="text-right py-3 px-4 font-medium text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {uploads.map((upload) => (
                    <tr key={upload.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                            <FileText className="h-5 w-5 text-blue-600" />
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">{upload.filename}</div>
                            <div className="text-sm text-gray-600 capitalize">{upload.file_type}</div>
                          </div>
                        </div>
                      </td>
                      
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(upload.status)}
                          <span className={`
                            inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize
                            ${getStatusColor(upload.status)}
                          `}>
                            {upload.status}
                          </span>
                        </div>
                      </td>
                      
                      <td className="py-4 px-4 text-gray-600">
                        {formatFileSize(upload.file_size)}
                      </td>
                      
                      <td className="py-4 px-4 text-gray-600">
                        {formatRelativeTime(upload.created_at)}
                      </td>
                      
                      <td className="py-4 px-4">
                        <div className="flex items-center justify-end gap-2">
                          {upload.status === 'failed' && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleReprocess(upload.id)}
                            >
                              <RefreshCw className="h-4 w-4" />
                            </Button>
                          )}
                          
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleDelete(upload.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No files uploaded</h3>
              <p className="text-gray-600">Upload your first document to get started with AI learning</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Usage Tips */}
      <Card>
        <CardHeader>
          <CardTitle>Tips for Better Results</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Supported Formats</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• PDF documents with text content</li>
                <li>• Microsoft Word documents (.docx)</li>
                <li>• Plain text files (.txt)</li>
              </ul>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Best Practices</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Use clear, well-structured documents</li>
                <li>• Ensure text is readable and not image-based</li>
                <li>• Keep files under 10MB for faster processing</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
