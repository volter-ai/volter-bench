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
  collections: {
    creatures: BaseEntity[];
  };
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

  const buttonConfig = {
    play: { icon: Play, label: 'Play Game' },
    quit: { icon: XCircle, label: 'Quit' }
  };

  return (
    <Card className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-slate-800 to-slate-900 aspect-video rounded-none border-0">
      <div className="w-full flex-1 flex items-center justify-center pt-16">
        <h1 className="text-6xl font-bold text-white tracking-wider">
          CREATURE BATTLE
        </h1>
      </div>

      <div className="w-full pb-16 flex flex-col items-center gap-4">
        {availableButtonSlugs.map(slug => {
          if (!(slug in buttonConfig)) return null;
          
          const { icon: Icon, label } = buttonConfig[slug as keyof typeof buttonConfig];
          
          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              variant="secondary"
              size="lg"
              className="min-w-[200px] gap-2"
            >
              <Icon className="w-5 h-5" />
              <span>{label}</span>
            </Button>
          );
        })}
      </div>
    </Card>
  );
}
