import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButtons = () => {
    const buttonConfig = [
      { id: 'play', label: 'Play', icon: <Play className="mr-2" /> },
      { id: 'quit', label: 'Quit', icon: <X className="mr-2" /> },
    ];

    return buttonConfig.map((button) => {
      if (availableButtonSlugs.includes(button.id)) {
        return (
          <button
            key={button.id}
            onClick={() => emitButtonClick(button.id)}
            className="flex items-center justify-center px-6 py-3 mb-4 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-300"
          >
            {button.icon}
            {button.label}
          </button>
        );
      }
      return null;
    });
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-[177.78vh] max-h-[56.25vw] aspect-video flex flex-col items-center justify-between p-8">
        <h1 className="text-5xl font-bold text-white mt-16">
          {data?.display_name || "Game Title"}
        </h1>
        <div className="flex flex-col items-center mb-16">
          {renderButtons()}
        </div>
      </div>
    </div>
  );
}
