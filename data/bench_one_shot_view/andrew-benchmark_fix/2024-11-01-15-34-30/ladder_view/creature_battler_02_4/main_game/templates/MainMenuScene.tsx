import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Creature {
  uid: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
  display_name: string;
  description: string;
}

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: {
    prototype_id: string;
    category: string;
  };
  entities: Record<string, any>;
  collections: {
    creatures: Creature[];
  };
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButtons = () => {
    return (
      <div className="flex space-x-4">
        {availableButtonSlugs.includes('play') && (
          <Button
            onClick={() => emitButtonClick('play')}
            className="flex items-center space-x-2"
          >
            <Play size={20} />
            <span>Play</span>
          </Button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            onClick={() => emitButtonClick('quit')}
            variant="destructive"
            className="flex items-center space-x-2"
          >
            <X size={20} />
            <span>Quit</span>
          </Button>
        )}
      </div>
    );
  };

  return (
    <Card className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-4xl font-bold text-white mt-16">
        {data?.display_name || 'Game Title'}
      </h1>
      <div className="flex-grow" />
      {renderButtons()}
      {data?.entities?.player && (
        <div className="text-white text-sm mt-4">
          Player: {data.entities.player.display_name}
        </div>
      )}
    </Card>
  );
}
