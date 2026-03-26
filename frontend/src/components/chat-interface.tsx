"use client";

import { useRef, useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Send, Bot, User, Wrench } from "lucide-react";
import { sendMessageStream, type ChatStreamEvent } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  toolsUsed?: string[];
}

const INITIAL_MESSAGES: Message[] = [
  {
    role: "assistant",
    content:
      "Hello! I'm your DevOps AI Agent. I can help you manage services, containers, deployments, and analyze logs. Try asking me something like:\n\n- \"List my running containers\"\n- \"Check the health of web-api\"\n- \"Analyze logs for the backend service\"\n- \"Deploy myapp:latest to staging\"",
  },
];

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, status]);

  const handleEvent = useCallback((event: ChatStreamEvent) => {
    switch (event.type) {
      case "conversation_id":
        setConversationId(event.data as string);
        break;
      case "status":
        setStatus(event.data as string);
        break;
      case "tools_used":
        setStatus(`Using tools: ${(event.data as string[]).join(", ")}`);
        break;
      case "content": {
        const content = event.data as string;
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content },
        ]);
        setStatus(null);
        break;
      }
      case "done":
        setIsLoading(false);
        setStatus(null);
        break;
      case "error":
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `Error: ${event.data}. Make sure the backend is running and API keys are configured.`,
          },
        ]);
        setIsLoading(false);
        setStatus(null);
        break;
    }
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setIsLoading(true);
    setStatus("thinking");

    try {
      await sendMessageStream(trimmed, conversationId, handleEvent);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Could not connect to the backend. Make sure the FastAPI server is running on http://localhost:8000",
        },
      ]);
      setIsLoading(false);
      setStatus(null);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Messages */}
      <ScrollArea className="flex-1 p-4">
        <div className="mx-auto flex max-w-3xl flex-col gap-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 ${
                msg.role === "user" ? "flex-row-reverse" : ""
              }`}
            >
              <div className="flex size-8 shrink-0 items-center justify-center rounded-md bg-muted">
                {msg.role === "assistant" ? (
                  <Bot className="size-4" />
                ) : (
                  <User className="size-4" />
                )}
              </div>
              <div className="flex flex-col gap-1">
                <div
                  className={`rounded-lg px-3 py-2 text-sm leading-relaxed whitespace-pre-wrap ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  {msg.content}
                </div>
                {msg.toolsUsed && msg.toolsUsed.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {msg.toolsUsed.map((tool) => (
                      <Badge key={tool} variant="outline" className="text-xs">
                        <Wrench className="mr-1 size-3" />
                        {tool}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3">
              <div className="flex size-8 shrink-0 items-center justify-center rounded-md bg-muted">
                <Bot className="size-4 animate-pulse" />
              </div>
              <div className="rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">
                {status === "thinking" && "Thinking..."}
                {status?.startsWith("Using tools") && (
                  <span className="flex items-center gap-1">
                    <Wrench className="size-3 animate-spin" />
                    {status}
                  </span>
                )}
                {!status && "Processing..."}
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </ScrollArea>

      <Separator />

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4">
        <div className="mx-auto flex max-w-3xl gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask the DevOps AI Agent..."
            className="min-h-[44px] max-h-32 resize-none"
            rows={1}
          />
          <Button type="submit" size="icon" disabled={isLoading || !input.trim()}>
            <Send className="size-4" />
          </Button>
        </div>
      </form>
    </div>
  );
}
