import fs from 'fs';
import path from 'path';

function getGitRoot() {
    let currentPath = __dirname;
    while (!fs.existsSync(path.join(currentPath, '.git'))) {
        currentPath = path.join(currentPath, '..');
    }
    return currentPath;
}

export function listConversations() {
    const root = getGitRoot();
    const types = fs.readdirSync(root + '/output/report_output');
    return Object.fromEntries(types.map(type => {
        const files = fs.readdirSync(root + '/output/report_output/' + type);
        return [type, files];
    }
    ));
}

export function getConversationPath(id, type = null) {
    const root = getGitRoot();
    const types = fs.readdirSync(root + '/output/report_output');
    if (type === null) {
        for (const t of types) {
            const files = fs.readdirSync(root + '/output/report_output/' + t);
            if (files.includes(id)) {
                type = t;
                break;
            }
        }
    }
    if (type === null) {
        return null;
    }
    return root + '/output/report_output/' + type + '/' + id;
}

export function getConversation(id, type = null) {
    function getJsonOrNull(path) {
        try {
            return JSON.parse(fs.readFileSync(path));
        }
        catch (e) {
            return null;
        }
    }

    const path = getConversationPath(id, type);
    const config = getJsonOrNull(path + '/config.json');
    const history = getJsonOrNull(path + '/history.json');
    const analysis = getJsonOrNull(path + '/gpt4_analysis.json');

    return {
        config,
        history,
        analysis,
    }
}

