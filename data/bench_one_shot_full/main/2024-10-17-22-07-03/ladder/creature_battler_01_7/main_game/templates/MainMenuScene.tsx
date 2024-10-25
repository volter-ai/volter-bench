import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

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

export function MainMenuSceneView(props: { data: GameUIData; uid: string }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const handleButtonClick = (slug: string) => {
    emitButtonClick(slug);
  };

  return (
    <div className="w-full h-screen bg-gradient-to-b from-blue-900 to-blue-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
        {props.data.display_name || "Game Title"}
      </h1>

      <div className="flex flex-col space-y-4">
        {availableButtonSlugs.includes('play') && (
          <button
            onClick={() => handleButtonClick('play')}
            className="flex items-center justify-center space-x-2 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 ease-in-out"
          >
            <Play size={24} />
            <span>Play</span>
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            onClick={() => handleButtonClick('quit')}
            className="flex items-center justify-center space-x-2 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 ease-in-out"
          >
            <X size={24} />
            <span>Quit</span>
          </button>
        )}
      </div>

      <div className="text-white text-sm mt-8">
        {props.data.description || "Welcome to the game!"}
      </div>
    </div>
  )
}
