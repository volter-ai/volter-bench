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
  display_name: string;
}

type ButtonConfig = {
  [key: string]: {
    text: string;
    icon: React.ComponentType<{ size?: number }>;
  };
};

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig: ButtonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-blue-700 flex flex-col items-center justify-between p-8">
      <div className="w-full h-1/3 flex items-center justify-center">
        <div className="bg-white bg-opacity-20 p-8 rounded-lg">
          <h1 className="text-4xl font-bold text-white">
            {props.data.display_name || "Untitled Game"}
          </h1>
        </div>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug];
          if (!config) return null;

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-bold py-2 px-4 rounded-full flex items-center space-x-2 transition-all duration-200"
            >
              {config.icon && <config.icon size={24} />}
              <span>{config.text}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
