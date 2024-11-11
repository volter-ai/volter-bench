import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface PlayerStats {
  stat1: number;
}

interface Player {
  uid: string;
  stats: PlayerStats;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center tracking-wider">
            GAME TITLE
          </h1>
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 w-full max-w-md">
          {availableButtonSlugs.includes('play-game') && (
            <button
              onClick={() => emitButtonClick('play-game')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg text-xl transition-colors"
            >
              <Play className="w-6 h-6" />
              Play Game
            </button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xl transition-colors"
            >
              <XCircle className="w-6 h-6" />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
