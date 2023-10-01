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
    conversationList,
    onSelect
}) {
    const types = Object.keys(conversationList);
    return (<>
        <Select
            placeholder="Select an option"
            className="max-w-sm"
            variant="flat"
            onSelectionChange={(elem) => {
                const item = [...elem].pop();
                const [type, file] = item.split('/');
                console.log(type, file);
                onSelect(type, file);
            }}
        >
            {types.map(type =>
                <SelectSection key={type} label={type}>
                    {conversationList[type].map(file =>
                        <SelectItem key={`${type}/${file}`} value={`${type}/${file}`}>
                            {formatFileName(file, type)}
                        </SelectItem>
                    )}
                </SelectSection>
            )}
        </Select>
    </>)
}

export function ConversationShowcase({ conversationList }) {
    const initialConversation = useMemo(() => {
        return {
            type: Object.keys(conversationList)[0],
            file: conversationList[Object.keys(conversationList)[0]][0],
        };
    }, [conversationList])
    const [selectedConversation, setSelectedConversation] = React.useState(initialConversation);
    const [conversation, setConversation] = React.useState(null);

    useEffect(() => {
        const { type, file } = selectedConversation;
        fetch(`/api/conversation/${file}`).then(res => res.json()).then(data => {
            ;
            setConversation(data);
        });
    }, [selectedConversation]);

    return (<>
        <div className='flex flex-col gap-4'>
            <ConversationSelect
                conversationList={conversationList}
                onSelect={(type, file) => setSelectedConversation({ type: type, file: file })}
            />
            <Chat data={conversation?.history} config={conversation?.config} />
        </div>
    </>);
}