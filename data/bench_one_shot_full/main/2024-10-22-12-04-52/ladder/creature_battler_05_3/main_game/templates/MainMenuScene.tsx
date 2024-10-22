import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X, Settings, HelpCircle } from 'lucide-react';

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
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
    settings: { text: 'Settings', icon: Settings },
    help: { text: 'Help', icon: HelpCircle },
  };

  return (
    <div className="w-full h-full bg-gray-800 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="w-full h-1/3 bg-gray-700 flex items-center justify-center rounded-lg">
        <h1 className="text-4xl font-bold text-white">Game Title</h1>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded flex items-center space-x-2"
            >
              <config.icon className="w-5 h-5" />
              <span>{config.text}</span>
            </button>
          );
        })}
      </div>

      <div className="text-white text-sm">
        Player: {props.data.entities.player?.display_name ?? 'Unknown'}
      </div>
    </div>
  );
}
