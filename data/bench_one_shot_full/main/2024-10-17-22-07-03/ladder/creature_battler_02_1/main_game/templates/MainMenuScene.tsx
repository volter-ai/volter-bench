import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const renderButtons = () => {
    const buttons = [
      { id: 'play', label: 'Play', icon: <Play size={24} /> },
      { id: 'quit', label: 'Quit', icon: <X size={24} /> },
    ];

    return (
      <div className="flex flex-col space-y-4">
        {buttons.map((button) => (
          availableButtonSlugs.includes(button.id) && (
            <button
              key={button.id}
              onClick={() => emitButtonClick(button.id)}
              className="flex items-center justify-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
            >
              {button.icon}
              <span>{button.label}</span>
            </button>
          )
        ))}
      </div>
    );
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-purple-800 to-blue-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-4xl md:text-6xl font-bold text-white mt-16">
        {props.data.display_name || "Game Title"}
      </div>
      <div className="mb-16">
        {renderButtons()}
      </div>
    </div>
  );
}
