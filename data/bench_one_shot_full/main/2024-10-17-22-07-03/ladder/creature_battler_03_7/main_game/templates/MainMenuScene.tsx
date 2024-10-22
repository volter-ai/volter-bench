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

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const isButtonAvailable = (slug: string) => availableButtonSlugs.includes(slug);

  return (
    <div className="w-full h-full flex flex-col justify-between items-center bg-gradient-to-b from-blue-500 to-purple-600 p-8">
      <div className="flex-1 flex items-center">
        <h1 className="text-6xl font-bold text-white text-center">
          {props.data.display_name || "Game Title"}
        </h1>
      </div>

      <div className="flex flex-col items-center space-y-4">
        {isButtonAvailable('play') && (
          <button
            onClick={() => emitButtonClick('play')}
            className="flex items-center justify-center w-48 h-12 bg-green-500 hover:bg-green-600 text-white font-bold rounded-full transition duration-300 ease-in-out"
          >
            <Play className="mr-2" size={24} />
            Play
          </button>
        )}
        {isButtonAvailable('quit') && (
          <button
            onClick={() => emitButtonClick('quit')}
            className="flex items-center justify-center w-48 h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded-full transition duration-300 ease-in-out"
          >
            <X className="mr-2" size={24} />
            Quit
          </button>
        )}
      </div>

      <div className="mt-8 text-white text-sm">
        {props.data.entities.player && (
          <p>Welcome, {props.data.entities.player.display_name}!</p>
        )}
      </div>
    </div>
  )
}
