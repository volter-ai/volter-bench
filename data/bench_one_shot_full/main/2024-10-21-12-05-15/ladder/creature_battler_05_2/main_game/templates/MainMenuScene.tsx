import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerName = props.data.entities.player?.display_name || "Player";

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full h-full max-w-[177.78vh] max-h-[56.25vw] flex flex-col items-center justify-between p-8">
        <h1 className="text-5xl font-bold text-white mt-16">Creature Battle Game</h1>
        
        <div className="text-2xl text-white mb-8">
          Welcome, {playerName}!
        </div>

        <div className="flex flex-col items-center mb-16 space-y-4">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center w-48 h-12 bg-green-500 hover:bg-green-600 text-white font-bold rounded-full transition duration-200"
            >
              <Play className="mr-2" size={24} />
              Play
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center w-48 h-12 bg-red-500 hover:bg-red-600 text-white font-bold rounded-full transition duration-200"
            >
              <X className="mr-2" size={24} />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
