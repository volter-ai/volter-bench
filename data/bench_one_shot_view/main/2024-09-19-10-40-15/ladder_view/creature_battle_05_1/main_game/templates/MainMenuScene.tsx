import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const handleButtonClick = (buttonId: string) => {
    if (currentButtonIds.includes(buttonId)) {
      emitButtonClick(buttonId);
    }
  };

  return (
    <div className="cq-h-full cq-w-full cq-flex cq-flex-col cq-justify-between cq-items-center cq-p-8 cq-bg-gray-100">
      <div className="cq-w-full cq-flex cq-justify-center cq-items-center cq-mb-8">
        <Card className="cq-w-3/4 cq-h-40 cq-flex cq-justify-center cq-items-center cq-bg-blue-500 cq-text-white">
          <h1 className="cq-text-4xl cq-font-bold">Game Title</h1>
        </Card>
      </div>

      <div className="cq-w-full cq-flex cq-flex-col cq-items-center cq-space-y-4">
        <Button
          className="cq-w-48 cq-h-12 cq-text-lg"
          onClick={() => handleButtonClick('play')}
          disabled={!currentButtonIds.includes('play')}
        >
          <Play className="cq-mr-2" /> Play
        </Button>
        <Button
          className="cq-w-48 cq-h-12 cq-text-lg"
          onClick={() => handleButtonClick('quit')}
          disabled={!currentButtonIds.includes('quit')}
        >
          <X className="cq-mr-2" /> Quit
        </Button>
      </div>

      {props.data.entities.player && (
        <Alert className="cq-mt-8">
          <AlertTitle>Welcome, {props.data.entities.player.display_name}!</AlertTitle>
          <AlertDescription>{props.data.entities.player.description}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
