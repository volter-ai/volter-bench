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
      
      <Card className="cq-w-full cq-max-w-md cq-p-4 cq-mb-8">
        <div className="cq-flex cq-flex-col cq-gap-4">
          <Button
            onClick={() => handleButtonClick('play')}
            disabled={!availableButtonSlugs.includes('play')}
            className="cq-w-full"
          >
            <Play className="cq-mr-2" /> Play
          </Button>
          <Button
            onClick={() => handleButtonClick('quit')}
            disabled={!availableButtonSlugs.includes('quit')}
            className="cq-w-full"
          >
            <X className="cq-mr-2" /> Quit
          </Button>
        </div>
      </Card>
      
      {props.data.entities.player && (
        <Alert className="cq-mt-4">
          <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
          <AlertDescription>{props.data.entities.player.description}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
