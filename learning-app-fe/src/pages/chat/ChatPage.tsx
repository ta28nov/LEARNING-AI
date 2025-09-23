import React, { useEffect, useState } from 'react';
import { Send, Plus, MessageCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useChatStore } from '@/stores/chatStore';
import { formatRelativeTime } from '@/lib/utils';

export function ChatPage() {
  const { 
    sessions, 
    currentSession, 
    messages, 
    fetchSessions, 
    createSession, 
    selectSession,
    sendMessage,
    isSendingMessage
  } = useChatStore();
  
  const [messageInput, setMessageInput] = useState('');
  const [chatMode, setChatMode] = useState<'strict' | 'hybrid'>('hybrid');

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  const handleCreateSession = async () => {
    try {
      await createSession({
        title: `Chat Session ${sessions.length + 1}`,
        mode: chatMode
      });
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim() || !currentSession) return;

    try {
      await sendMessage(currentSession.id, messageInput);
      setMessageInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="p-6 h-[calc(100vh-6rem)]">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-full">
        {/* Sidebar - Chat Sessions */}
        <div className="lg:col-span-1">
          <Card className="h-full">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Chat Sessions</CardTitle>
                <Button size="sm" onClick={handleCreateSession}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {sessions.map((session) => (
                  <div
                    key={session.id}
                    onClick={() => selectSession(session.id)}
                    className={`
                      p-3 rounded-lg cursor-pointer transition-colors
                      ${currentSession?.id === session.id 
                        ? 'bg-primary-50 border border-primary-200' 
                        : 'hover:bg-gray-50'
                      }
                    `}
                  >
                    <h4 className="font-medium text-gray-900">{session.title}</h4>
                    <p className="text-xs text-gray-600">{formatRelativeTime(session.created_at)}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Chat Area */}
        <div className="lg:col-span-3">
          {currentSession ? (
            <Card className="h-full flex flex-col">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>{currentSession.title}</CardTitle>
                  <select
                    value={chatMode}
                    onChange={(e) => setChatMode(e.target.value as 'strict' | 'hybrid')}
                    className="px-3 py-1 border border-gray-300 rounded-lg text-sm"
                  >
                    <option value="hybrid">Hybrid Mode</option>
                    <option value="strict">Strict Mode</option>
                  </select>
                </div>
              </CardHeader>
              
              <CardContent className="flex-1 flex flex-col">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`
                          max-w-xs lg:max-w-md px-4 py-2 rounded-lg
                          ${message.sender === 'user'
                            ? 'bg-primary-600 text-white'
                            : 'bg-gray-100 text-gray-900'
                          }
                        `}
                      >
                        <p className="text-sm">{message.message}</p>
                      </div>
                    </div>
                  ))}
                  
                  {isSendingMessage && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 px-4 py-2 rounded-lg">
                        <LoadingSpinner size="sm" />
                      </div>
                    </div>
                  )}
                </div>

                {/* Message Input */}
                <form onSubmit={handleSendMessage} className="flex gap-2">
                  <Input
                    value={messageInput}
                    onChange={(e) => setMessageInput(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-1"
                  />
                  <Button type="submit" disabled={!messageInput.trim() || isSendingMessage}>
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </CardContent>
            </Card>
          ) : (
            <Card className="h-full flex items-center justify-center">
              <CardContent className="text-center">
                <MessageCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Start a Conversation</h3>
                <p className="text-gray-600 mb-4">Create a new chat session to begin</p>
                <Button onClick={handleCreateSession}>
                  <Plus className="h-4 w-4 mr-2" />
                  New Chat
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
