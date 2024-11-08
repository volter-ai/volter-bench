import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  __type: 'Player';
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  if (!props.data) {
    return null;
  }

  return (
    <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-800 to-slate-900">
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
        {/* Title Section with Image */}
        <div className="flex-1 flex items-center justify-center w-full">
          <div 
            className="w-full max-w-2xl h-32 bg-contain bg-center bg-no-repeat"
            style={{ backgroundImage: `url(/assets/title.png)` }}
            aria-label={props.data.display_name || "Game Title"}
          />
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 mb-16 w-full max-w-md">
          {availableButtonSlugs.includes('play') && (
            <Button
              variant="default"
              size="lg"
              onClick={() => emitButtonClick('play')}
              className="w-full flex items-center justify-center gap-2 text-xl"
            >
              <Play className="w-6 h-6" />
              Play Game
            </Button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <Button
              variant="destructive"
              size="lg"
              onClick={() => emitButtonClick('quit')}
              className="w-full flex items-center justify-center gap-2 text-xl"
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
