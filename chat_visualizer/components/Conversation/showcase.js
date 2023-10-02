"use client"
import React, { useMemo, useEffect } from "react";
import { Select, SelectSection, SelectItem } from "@nextui-org/react";
import { Chat } from "../chat";

function formatFileName(file, type = null) {
    // Here is an examples : A_gpt-3.5-turbo_D_gpt-3.5-turbo_hard_20231001_214017 or A_gpt-3.5-turbo_I_gpt-3.5-turbo_D_gpt-3.5-turbo_hard_20231001_214017
    // const regex = /([AID])_([a-zA-Z0-9-]+)/g;
    // const matches = [...file.matchAll(regex)];
    // const models = matches.map(match => match[2]);
    // const modelString = models.map(model => `${model} (${model.charAt(0)})`).join(' - ');
    const splits = file.split('_');
    let models = []
    for (let i = 0; i < splits.length; i += 2) {
        switch (splits[i]) {
            case 'A':
            case 'I':
            case 'D':
                models.push(`${splits[i + 1]} (${splits[i]})`);
                break;
                break;
            default:
                break;
        }
    }
    return models.join(' <=> ');
}

function ConversationSelect({
    conversations,
    onSelect
}) {
    const types = Object.keys(conversations);
    return (<>
        <Select
            placeholder="Select an conversation"
            className="max-w-sm"
            selectedKeys={[`${types[0]}/${conversations[types[0]][0].file}`]}
            onSelectionChange={(elem) => {
                const item = [...elem].pop();
                const [type, file] = item.split('/');
                console.log(type, file);
                onSelect(type, file);
            }}
        >
            {types.map(type =>
                <SelectSection key={type} label={type}>
                    {conversations[type].map(conv =>
                        <SelectItem key={`${type}/${conv.file}`} value={`${type}/${conv.file}`}>
                            {formatFileName(conv.file, type)}
                        </SelectItem>
                    )}
                </SelectSection>
            )}
        </Select>
    </>)
}

export function ConversationShowcase({ conversations }) {
    const initialConversation = useMemo(() => {
        return {
            type: Object.keys(conversations)[0],
            file: conversations[Object.keys(conversations)[0]][0].file,
        };
    }, [conversations])
    const [selectedConversation, setSelectedConversation] = React.useState(initialConversation);
    const [conversation, setConversation] = React.useState(null);

    useEffect(() => {
        const { type, file } = selectedConversation;
        fetch(`/api/conversation?type=${type}&id=${file}`).then(res => res.json()).then(data => {
            setConversation(data);
        });
    }, [selectedConversation]);

    return (<>
        <div className='flex flex-col gap-4 w-full sm:w-5/6 mx-auto'>
            <div className='flex flex-row justify-end'>
                <ConversationSelect
                    conversations={conversations}
                    onSelect={(type, file) => setSelectedConversation({ type: type, file: file })}
                />
            </div>
                <Chat data={conversation?.history} config={conversation?.config} />
        </div>
    </>);
}