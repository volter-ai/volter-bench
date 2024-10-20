import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any>;
      display_name: string;
      description: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const handleButtonClick = (slug: string) => {
    emitButtonClick(slug);
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] aspect-video bg-black bg-opacity-50 text-white p-8 flex flex-col justify-between">
        <div className="text-center">
          <h1 className="text-6xl font-bold mb-4">Creature Battle</h1>
          <p className="text-xl">Welcome, {props.data.entities.player?.display_name || 'Player'}!</p>
        </div>
        
        <div className="flex flex-col items-center">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => handleButtonClick('play')}
              className="flex items-center justify-center w-48 h-12 mb-4 bg-green-500 hover:bg-green-600 text-white font-bold rounded"
            >
              <Play className="mr-2" size={20} />
              Play
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => handleButtonClick('quit')}
              className="flex items-center justify-center w-48 h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded"
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
