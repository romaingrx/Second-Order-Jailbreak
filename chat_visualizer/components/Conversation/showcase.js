"use client";
import React, { useMemo, useEffect, useCallback } from "react";
import { Select, SelectSection, SelectItem, Spinner } from "@nextui-org/react";
import { Chat } from "../chat";
import Link from "next/link";
import { useParams } from "next/navigation";

function formatFileName(file, type = null) {
  // Here is an examples : A_gpt-3.5-turbo_D_gpt-3.5-turbo_hard_20231001_214017 or A_gpt-3.5-turbo_I_gpt-3.5-turbo_D_gpt-3.5-turbo_hard_20231001_214017
  // const regex = /([AID])_([a-zA-Z0-9-]+)/g;
  // const matches = [...file.matchAll(regex)];
  // const models = matches.map(match => match[2]);
  // const modelString = models.map(model => `${model} (${model.charAt(0)})`).join(' - ');
  const splits = file.split("_");
  let models = [];
  for (let i = 0; i < splits.length; i += 2) {
    switch (splits[i]) {
      case "A":
      case "I":
      case "D":
        models.push(`${splits[i + 1]} (${splits[i]})`);
        break;
        break;
      default:
        break;
    }
  }
  return models.join(" <=> ");
}

function ConversationSelect({ conversations, onSelect, setLink }) {
  const types = Object.keys(conversations);

  let selectedItems = null;
  const params = useParams();
  if (params.type && params.file) {
    selectedItems = [`${params.type}/${params.file}`];
  }

  return (
    <>
      <Select
        items={conversations}
        placeholder="Select an conversation"
        className="max-w-sm"
        selectedKeys={selectedItems}
        onSelectionChange={(elem) => {
          const item = [...elem].pop();
          const [type, file] = item.split("/");
          !setLink && onSelect(type, file);
        }}
      >
        {types.map((type) => (
          <SelectSection key={type} label={type}>
            {conversations[type].map((conv) => (
              <SelectItem
                key={`${type}/${conv.file}`}
                textValue={formatFileName(conv.file, type)}
              >
                {setLink ? (
                  <Link href={`/${type}/${conv.file}`}>
                    {formatFileName(conv.file, type)}
                  </Link>
                ) : (
                  formatFileName(conv.file, type)
                )}
              </SelectItem>
            ))}
          </SelectSection>
        ))}
      </Select>
    </>
  );
}

export function ConversationShowcase({
  conversations,
  initialConversation,
  onSelectRedirect,
}) {
  initialConversation = useMemo(() => {
    return (
      initialConversation || {
        type: Object.keys(conversations)[0],
        file: conversations[Object.keys(conversations)[0]][0].file,
      }
    );
  }, [conversations]);
  const [selectedConversation, setSelectedConversation] =
    React.useState(initialConversation);
  const [conversation, setConversation] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(true);

  useEffect(() => {
    setIsLoading(true);
    const { type, file } = selectedConversation;
    console.log(type, file);
    fetch(`/api/conversation?type=${type}&id=${file}`)
      .then((res) => res.json())
      .then((data) => {
        setConversation(data);
        setIsLoading(false);
      });
  }, [selectedConversation]);

  const onSelect = useCallback(
    (type, file) => {
      setSelectedConversation({ type, file });
    },
    [setSelectedConversation, onSelectRedirect]
  );

  return (
    <>
      <div className="flex flex-col gap-4 w-full sm:w-5/6 mx-auto">
        <div className="flex flex-row justify-end">
          <ConversationSelect
            conversations={conversations}
            onSelect={onSelect}
            setLink={onSelectRedirect}
          />
        </div>
        {isLoading ? (
          <div className="flex flex-col justify-center items-center mx-auto">
            <Spinner color="secondary"/>
            <p className="text-gray-500">Loading conversation...</p>
          </div>
        ) : (
          <Chat data={conversation?.history} config={conversation?.config} />
        )}
      </div>
    </>
  );
}
