import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

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
  display_name?: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { label: "Play", icon: Play },
    quit: { label: "Quit", icon: X },
  };

  const gameTitle = data?.display_name || data?.entities?.player?.display_name || "Creature Adventure";

  if (!data) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16 text-center">
        {gameTitle}
      </div>

      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-purple-600 font-bold py-3 px-6 rounded-full shadow-lg hover:bg-purple-100 transition duration-300 flex items-center justify-center space-x-2"
            >
              <config.icon className="w-6 h-6" />
              <span>{config.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
