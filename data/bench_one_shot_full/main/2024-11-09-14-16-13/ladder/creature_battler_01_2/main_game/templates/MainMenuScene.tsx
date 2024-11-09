import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  __type: "Player";
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const isButtonAvailable = (slug: string) => 
    availableButtonSlugs?.includes(slug);

  return (
    <Card 
      className="relative w-full" 
      style={{ paddingBottom: '56.25%' }}
      uid={props.data?.uid}
    >
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
        
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            GAME TITLE
          </h1>
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 w-full max-w-md">
          {isButtonAvailable('play') && (
            <Button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center gap-2 w-full py-8 bg-green-600 hover:bg-green-700 
                         text-white rounded-lg transition-colors duration-200"
              uid={`${props.data?.uid}-play`}
              variant="default"
              size="lg"
            >
              <Play className="w-6 h-6" />
              <span className="text-xl">Play Game</span>
            </Button>
          )}

          {isButtonAvailable('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center gap-2 w-full py-8 bg-red-600 hover:bg-red-700 
                         text-white rounded-lg transition-colors duration-200"
              uid={`${props.data?.uid}-quit`}
              variant="destructive"
              size="lg"
            >
              <XCircle className="w-6 h-6" />
              <span className="text-xl">Quit</span>
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
