import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Card } from "@/components/ui/card";

// Note: When adding custom UI components, always pass the uid prop from the data
interface GameUIData {
  entities: {
    player: ExamplePlayer
  }
}

interface ExamplePlayer {
  uid: string,
  stats: {
    stat1: number,
  },
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <Card className="w-full h-full">
      {/* 16:9 Container */}
      <div className="absolute inset-0 flex flex-col items-center justify-between py-12 aspect-video max-h-full max-w-full mx-auto">
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold tracking-wider">
            GAME TITLE
          </h1>
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 items-center mb-8">
          {availableButtonSlugs?.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center gap-2 px-8 py-4 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg text-xl transition-colors"
            >
              <Play size={24} />
              <span>Play Game</span>
            </button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center gap-2 px-8 py-4 bg-destructive hover:bg-destructive/90 text-destructive-foreground rounded-lg text-xl transition-colors"
            >
              <XCircle size={24} />
              <span>Quit</span>
            </button>
          )}
        </div>
      </div>
    </Card>
  );
}
