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
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const gameTitle = props.data?.display_name || "Awesome Game";

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">{gameTitle}</h1>
        
        <div className="flex flex-col items-center space-y-4 mb-16">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center w-48 h-12 bg-green-500 hover:bg-green-600 text-white font-bold rounded-lg shadow-lg transition duration-300"
            >
              <Play className="mr-2" size={20} />
              Play
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center w-48 h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded-lg shadow-lg transition duration-300"
            >
              <X className="mr-2" size={20} />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
