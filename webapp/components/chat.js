import clsx from "clsx";
import Typewriter from "typewriter-effect";

const colors = {
  "pastel-0": "#BAABDA",
  "pastel-1": "#D6E5FA",
  "pastel-2": "#FFF9F9",
};

let agents = [];
function getIdx(name) {
  if (!agents.includes(name)) {
    agents.push(name);
  }
  return agents.indexOf(name);
}

function ChatBubble({ agent_name, timestamp, content, visible_to }) {
  const idx = getIdx(agent_name);
  const date = new Date(parseInt(timestamp) / 1000000).toLocaleString();

  let receivers = Array.isArray(visible_to)
    ? visible_to.filter((name) => name !== agent_name).join(", ")
    : visible_to;

  return (
    <div
      className={
        "flex flex-col rounded-lg shadow-lg overflow-hidden my-1 w-full bg-opacity-50"
      }
      style={{
        backgroundColor: colors["pastel-" + (idx % 3)],
      }}
    >
      <div className="flex flex-row items-center justify-between px-4 py-2">
        <div className="text-sm font-medium text-gray-900">
          {agent_name}
          {" -> "}
          {receivers}{" "}
        </div>
        <div className="text-xs text-gray-500">{date}</div>
      </div>
      <div className="px-4 py-2">
        <p className="text-sm text-gray-800">{content}</p>
      </div>
    </div>
  );
}

function AgentConfig({ name, role_desc, backend }) {
  const idx = getIdx(name);
  return (
    <>
      <div
        className={
          "text-md font-bold text-zinc-800 rounded-md p-1 w-fit bg-opacity-50"
        }
        style={{
          backgroundColor: colors["pastel-" + (idx % 3)],
        }}
      >
        {name}
      </div>
      <div className="px-4 py-2">
        <p className="text-sm text-gray-800">
          <strong>Role Description:</strong> {role_desc}
        </p>
      </div>
      <div className="px-4 py-2">
        <p className="text-sm text-gray-800 flex gap-1">
          <strong>Backend:</strong>
          <span>
            {Object.entries(backend).map(([key, value]) => (
              <Chip key={key}>{`${key}: ${JSON.stringify(value)}`}</Chip>
            ))}
          </span>
        </p>
      </div>
    </>
  );
}

export function Chip({ children, className = "" }) {
  return (
    <>
      <span className={clsx("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-blue-800 mr-2 mb-2", className)}>
        {children}
      </span>
    </>
  );
}

function Config({ name, global_prompt, environment, players, gpt4_analysis }) {
  return (
    <div className="flex flex-col rounded-lg shadow-lg overflow-hidden bg-white my-1 w-full my-2">
      <div className="text-lg font-bold text-gray-900 mx-auto">{name}</div>
      <div className="px-4 py-2 flex flex-wrap">
        {Object.entries(environment).map(([key, value]) => (
          <Chip key={key}>{`${key}: ${JSON.stringify(value)}`}</Chip>
        ))}
      </div>
      <div className="px-4">
        <p className="text-sm text-gray-800">
          <strong>Global Prompt:</strong> {global_prompt}
        </p>
      </div>
      <div className="px-4 py-2">
        {players.map((player) => (
          <AgentConfig {...player} key={player.name} />
        ))}
      </div>
      {gpt4_analysis && (
        <div className="px-4 py-2 rounded-md bg-blue-100/30 m-2">
          <p className="text-sm text-gray-800">
            <strong>GPT4 Analysis:</strong>
            <br />
            <div className="m-2">
              {typeof gpt4_analysis === "object" ? (
                Object.entries(gpt4_analysis).map(([key, value]) => (
                  <div
                    className="flex flex-row items-center align-center"
                    key={key}
                  >
                    <Chip>{`${key}`}</Chip>
                    <div className="" style={{ marginLeft: "5px" }}>
                      <Typewriter
                        onInit={(typewriter) => {
                          typewriter.typeString(value).start();
                        }}
                        options={{
                          delay: 5,
                        }}
                      />
                    </div>
                  </div>
                ))
              ) : (
                <Typewriter
                  onInit={(typewriter) => {
                    typewriter.typeString(gpt4_analysis).start();
                  }}
                  options={{
                    delay: 5,
                  }}
                />
              )}
            </div>
          </p>
        </div>
      )}
    </div>
  );
}

export function Chat({ conversation }) {
  const { history, config, analysis } = conversation;
  if (!conversation || !history || !config){
    return (
      <>
        <div className="flex flex-col items-center justify-center py-2 w-3/4 mx-auto my-5">
          <div className="text-lg font-bold text-gray-900 mx-auto">
            Couldn{"'"} retrieve conversation information
          </div>
        </div>
      </>
    );
  }
  let gpt4_analysis = null;
  if (analysis) {
    let gpt4_analysis_text = analysis.choices[0].message.content;
    try {
      gpt4_analysis = Object.fromEntries(
        gpt4_analysis_text.split("\n").map((line) => {
          const [key, value] = line.split(":");
          return [key.trim(), value.trim()];
        })
      );
    } catch (e) {
      gpt4_analysis = gpt4_analysis_text;
    }
  }

  return (
    <>
      <div className="flex flex-col">
        <Config {...config} gpt4_analysis={gpt4_analysis} />
        <div className="flex flex-col p-2">
          <div className="text-lg font-bold w-fit mx-4">History:</div>
          <div className="flex flex-col items-center justify-center min-h-screen w-[95%] mx-auto my-5">
            {history.map((item, index) => (
              <ChatBubble key={index} {...item} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
