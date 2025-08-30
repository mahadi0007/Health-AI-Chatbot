"use client"; // This is a client component, as it requires user interaction

import React, { useState, FormEvent, useRef, useEffect } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

// Define the structure of a message
interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // This ref will be attached to the <ScrollArea> component itself
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // This useEffect hook will run whenever messages change to scroll to the bottom
  useEffect(() => {
    // We find the specific viewport element that ShadCN creates inside the ScrollArea
    const viewport = scrollAreaRef.current?.querySelector('div[data-radix-scroll-area-viewport]');
    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight;
    }
  }, [messages, isLoading]); // Rerun when messages are added or loading state changes

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsLoading(true);
    const currentInput = input;
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: currentInput }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      const botMessage: Message = { role: "assistant", content: data.answer };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Failed to fetch from backend:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I'm having trouble connecting to the server. Please try again later.",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-8">
      <Card className="w-full max-w-2xl h-[85vh] flex flex-col">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">AI Chatbot For Cardio Health</CardTitle>
        </CardHeader>

        <CardContent className="flex-grow overflow-hidden">
          {/* We attach the ref to the parent ScrollArea component here */}
          <ScrollArea className="h-full" ref={scrollAreaRef}>
            <div className="space-y-4 pr-4">
              {messages.length === 0 && (
                <div className="text-center text-muted-foreground mt-8">
                  Ask me a question about the benefits of exercise!
                </div>
              )}
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex items-start gap-3 ${
                    message.role === "user" ? "justify-end" : ""
                  }`}
                >
                  {message.role === "assistant" && (
                    <Avatar className="h-8 w-8 border-2 border-indigo-500 p-1 rounded-full">
                      <AvatarFallback>AI</AvatarFallback>
                    </Avatar>
                  )}
                  <div
                    className={`rounded-lg px-4 py-2 max-w-[85%] whitespace-pre-wrap ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-secondary-foreground"
                    }`}
                  >
                    <p className="text-sm">{message.content}</p>
                  </div>
                   {message.role === "user" && (
                    <Avatar className="h-8 w-8 border-2 border-green-500 p-4 rounded-full">
                      <AvatarFallback>You</AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
              {isLoading && (
                 <div className="flex items-start gap-3">
                    <Avatar className="h-8 w-8 border-2 border-indigo-500 p-1 rounded-full">
                      <AvatarFallback>AI</AvatarFallback>
                    </Avatar>
                     <div className="rounded-lg px-4 py-2 bg-secondary text-secondary-foreground">
                        <p className="text-sm">Typing...</p>
                    </div>
                </div>
              )}
            </div>
          </ScrollArea>
        </CardContent>

        <CardFooter>
          <form onSubmit={handleSubmit} className="flex w-full items-center space-x-2">
            <Input
              id="message"
              placeholder="What are the benefits of strength training?"
              className="flex-1"
              autoComplete="off"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <Button type="submit" size="icon" disabled={isLoading}>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
              <span className="sr-only">Send</span>
            </Button>
          </form>
        </CardFooter>
      </Card>
    </main>
  );
}