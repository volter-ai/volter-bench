import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
      <h1 className="text-6xl font-bold mt-16">Game Title</h1>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;
          
          const Icon = config.icon;
          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-white text-blue-600 font-semibold py-3 px-6 rounded-full shadow-lg hover:bg-blue-100 transition duration-300 flex items-center space-x-2"
            >
              <Icon size={24} />
              <span>{config.text}</span>
            </button>
          );
        })}
      </div>

      <div className="absolute bottom-4 left-4 text-sm opacity-70">
        {props.data.entities.player?.display_name || 'Unknown Player'}
      </div>
    </div>
  );
}
