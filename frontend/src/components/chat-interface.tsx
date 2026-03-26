"use client";

import { useRef, useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Send, Bot, User } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const INITIAL_MESSAGES: Message[] = [
  {
    role: "assistant",
    content:
      "Hello! I'm your DevOps AI Agent. I can help you manage services, containers, deployments, and more. How can I assist you today?",
  },
];

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = { role: "user", content: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Placeholder response - will connect to backend later
    setTimeout(() => {
      const assistantMessage: Message = {
        role: "assistant",
        content:
          "I'm the DevOps AI Agent. Backend connection coming soon!",
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 800);
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
              <div
                className={`rounded-lg px-3 py-2 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-foreground"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3">
              <div className="flex size-8 shrink-0 items-center justify-center rounded-md bg-muted">
                <Bot className="size-4" />
              </div>
              <div className="rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">
                Thinking...
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
