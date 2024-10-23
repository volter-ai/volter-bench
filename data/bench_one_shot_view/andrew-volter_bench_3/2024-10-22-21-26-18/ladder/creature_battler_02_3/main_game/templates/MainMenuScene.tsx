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
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-900 text-white">
      <div className="w-full max-w-4xl aspect-video flex flex-col items-center justify-center space-y-8 p-8">
        <h1 className="text-5xl font-bold mb-8">{props.data.display_name || 'Main Menu'}</h1>
        <div className="flex flex-col space-y-4">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;
            const Icon = config.icon;
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center space-x-2 py-3 px-6 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors duration-200"
              >
                <Icon size={24} />
                <span>{config.text}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
