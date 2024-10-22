import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const isPlayAvailable = availableButtonSlugs.includes('play');
  const isQuitAvailable = availableButtonSlugs.includes('quit');

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-4xl aspect-video flex flex-col items-center justify-between p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-8">
          Creature Battle Game
        </h1>
        <div className="space-y-4">
          {isPlayAvailable && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center w-48 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              <Play className="mr-2" size={24} />
              Play
            </button>
          )}
          {isQuitAvailable && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center w-48 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
            >
              <X className="mr-2" size={24} />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
