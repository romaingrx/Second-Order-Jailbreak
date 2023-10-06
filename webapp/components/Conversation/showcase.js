"use client";
import React, { useMemo, useEffect, useCallback } from "react";
import { Select, SelectItem, Spinner, Chip, Tooltip } from "@nextui-org/react";
import { Chat } from "../chat";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Chip as ChatChip } from "../chat";

function formatFileName(file, type = null) {
  const splits = file.split("_");
  let models = [];
  for (let i = 0; i < splits.length; i += 2) {
    switch (splits[i]) {
      case "A":
      case "I":
      case "D":
        models.push(`${splits[i + 1]} (${splits[i]})`);
        break;
      default:
        break;
    }
  }
  return models.join(" <=> ");
}

function formatCategories(categories) {
  const keys = Object.keys(categories);
  const formattedKeys = keys.map((key) => {
    const letters = key.split("-");
    const formattedLetters = letters.map((letter) => letter[0].toUpperCase());
    return formattedLetters.join("");
  });
  return Object.fromEntries(
    keys.map((key, i) => [
      key,
      { value: categories[key], formatted: formattedKeys[i] },
    ]).filter(([, { value }]) => value !== "Not found")
  );
}

function SolveIcon({ solved }) {
  return (
    <svg width="20" height="20">
      <circle
        cx="10"
        cy="10"
        r="8"
        fill={solved ? "#4BB543" : "red"}
        fillOpacity="0.75"
      />
      {solved ? (
        <path
          d="M6 10 L9 13 L14 6"
          stroke="white"
          strokeWidth="2"
          fill="none"
        />
      ) : (
        <path
          d="M6 6 L14 14 M6 14 L14 6"
          stroke="white"
          strokeWidth="2"
          fill="none"
        />
      )}
    </svg>
  );
}

function ConversationPreview({ conversation }) {
  // Sow the models, if it succeeded or not, and the environment
  const { file, config, result } = conversation;
  const solved = result && result.solved === 'True'
  const environment = config && config.environment.env_type;
  const models_string = formatFileName(file);
  const categories =
    result && result.categories && formatCategories(result.categories);
  return (
    <>
      <div className="flex flex-row gap-2 items-center justify-start">
        <SolveIcon solved={solved} />
        <div className="flex flex-col gap-2 items-left text-xs">
          <div className="font-semibold">{models_string}</div>
          <div className="flex flex-row gap-0">
            {environment && (
              <ChatChip className="px-[0.3rem] py-[0.125rem] mx-0 my-0">
                {environment}
              </ChatChip>
            )}
            {categories &&
              Object.keys(categories).map((category) => (
                <Tooltip content="rpout" key={category} className="z-10">
                  <ChatChip className="px-[0.3rem] py-[0.125rem] mx-0 my-0">
                    {categories[category].formatted} {categories[category].value}
                  </ChatChip>
                </Tooltip>
              ))}
          </div>
        </div>
        <div />
      </div>
    </>
  );
}

function ConversationSelect({ conversations, onSelect, setLink }) {
  let selectedItems = null;
  const params = useParams();
  if (params.type && params.file) {
    selectedItems = [`${params.type}/${params.file}`];
  }

  const flatConvos = useMemo(() => {
    let flatConvos = [];
    for (const type of Object.keys(conversations)) {
      flatConvos.push(
        ...conversations[type].map((conversation) => ({
          ...conversation,
          type,
        }))
      );
    }
    return flatConvos;
  }, [conversations]);

  return (
    <>
      <Select
        items={flatConvos}
        renderValue={(items) => {
          return items.map((item) => {
            return (
              <ConversationPreview conversation={item.data} key={item.key} />
            );
          });
        }}
        placeholder="Select an conversation"
        className="max-w-sm"
        selectedKeys={selectedItems}
        onSelectionChange={(elem) => {
          const item = [...elem].pop();
          const [type, file] = item.split("/");
          !setLink && onSelect(type, file);
        }}
        style={{
          paddingTop: "1rem",
          paddingBottom: "1rem",
        }}
      >
        {(conversation) => {
          return (
            <SelectItem
              key={`${conversation.type}/${conversation.file}`}
              textValue={formatFileName(conversation.file, conversation.type)}
              data={conversation}
            >
              {setLink ? (
                <Link href={`/${conversation.type}/${conversation.file}`}>
                  <ConversationPreview conversation={conversation} />
                </Link>
              ) : (
                <ConversationPreview conversation={conversation} />
              )}
            </SelectItem>
          );
        }}
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
  }, [conversations, initialConversation]);
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
    [setSelectedConversation]
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
            <Spinner color="secondary" />
            <p className="text-gray-500">Loading conversation...</p>
          </div>
        ) : (
          <Chat conversation={conversation} />
        )}
      </div>
    </>
  );
}
