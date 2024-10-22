import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const handleButtonClick = (slug: string) => {
    if (availableButtonSlugs.includes(slug)) {
      emitButtonClick(slug);
    }
  };

  return (
    <div className="cq-h-full cq-w-full cq-flex cq-flex-col cq-justify-between cq-items-center cq-p-4 cq-bg-gray-100">
      <div className="cq-text-4xl cq-font-bold cq-text-center cq-mt-8">
        Game Title
      </div>
      
      <div className="cq-flex-grow"></div>
      
      <div className="cq-flex cq-flex-col cq-gap-4 cq-mb-8">
        <Button
          className={`cq-w-48 ${availableButtonSlugs.includes('play') ? '' : 'cq-opacity-50 cq-cursor-not-allowed'}`}
          onClick={() => handleButtonClick('play')}
          disabled={!availableButtonSlugs.includes('play')}
        >
          <Play className="cq-mr-2" /> Play
        </Button>
        <Button
          className={`cq-w-48 ${availableButtonSlugs.includes('quit') ? '' : 'cq-opacity-50 cq-cursor-not-allowed'}`}
          onClick={() => handleButtonClick('quit')}
          disabled={!availableButtonSlugs.includes('quit')}
        >
          <X className="cq-mr-2" /> Quit
        </Button>
      </div>
    </div>
  );
}
