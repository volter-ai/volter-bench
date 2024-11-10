import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Stats {
  hp?: number;
  max_hp?: number;
  attack?: number;
  defense?: number;
  sp_attack?: number;
  sp_defense?: number;
  speed?: number;
}

interface Meta {
  prototype_id: string;
  category: string;
  [key: string]: any;
}

interface BaseEntity {
  uid: string;
  __type: string;
  stats: Stats;
  meta: Meta;
  entities: Record<string, any>;
  collections: Record<string, any>;
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
          {availableButtonSlugs?.includes('play-game') && (
            <Button
              variant="default"
              size="lg"
              onClick={() => emitButtonClick('play-game')}
              className="w-full py-6 text-xl"
            >
              <Play className="w-6 h-6 mr-2" />
              Play Game
            </Button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <Button
              variant="destructive"
              size="lg"
              onClick={() => emitButtonClick('quit')}
              className="w-full py-6 text-xl"
            >
              <XCircle className="w-6 h-6 mr-2" />
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
