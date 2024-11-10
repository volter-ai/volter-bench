import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameUIData {
  entities: {
    player: {
      uid: string;
    };
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  if (!props.data?.entities?.player) {
    return null;
  }

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-slate-800 to-slate-900" role="main">
      <div className="w-full max-w-[177.78vh] aspect-video flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            GAME TITLE
          </h1>
        </div>

        <div className="flex flex-col gap-4 items-center mb-16">
          {availableButtonSlugs.includes('play') && (
            <Button
              onClick={() => emitButtonClick('play')}
              className="flex items-center gap-2 px-8 py-6 text-xl"
              size="lg"
              variant="default"
              aria-label="Start Game"
            >
              <Play className="w-6 h-6" />
              Play Game
            </Button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center gap-2 px-8 py-6 text-xl"
              size="lg"
              variant="destructive"
              aria-label="Quit Game"
            >
              <XCircle className="w-6 h-6" />
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
