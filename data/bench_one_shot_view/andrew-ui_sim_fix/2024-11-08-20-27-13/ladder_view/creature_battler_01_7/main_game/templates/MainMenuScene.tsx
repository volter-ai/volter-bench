import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface GameUIData {
  entities: {
    player?: {
      uid: string;
      // other fields optional since we don't use them in this view
    };
  };
  uid?: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  // Defensive check for required data
  if (!props?.data) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-slate-900">
        <p className="text-red-500">Error: Missing game data</p>
      </div>
    );
  }

  return (
    <div 
      className="w-full h-full flex items-center justify-center bg-gradient-to-b from-slate-800 to-slate-900"
      role="main"
      aria-label="Main Menu"
    >
      <div 
        className="w-full max-w-[177.78vh] aspect-video flex flex-col items-center justify-between p-8"
        key={props.data.uid}
      >
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            GAME TITLE
          </h1>
        </div>

        <div 
          className="flex flex-col gap-4 items-center mb-16"
          role="group"
          aria-label="Menu Options"
        >
          {availableButtonSlugs?.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-500 text-white rounded-lg text-xl transition-colors"
              aria-label="Play Game"
            >
              <Play className="w-6 h-6" aria-hidden="true" />
              <span>Play Game</span>
            </button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xl transition-colors"
              aria-label="Quit Game"
            >
              <XCircle className="w-6 h-6" aria-hidden="true" />
              <span>Quit</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
