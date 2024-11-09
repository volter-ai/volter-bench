import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react';
import {Button} from "@/components/ui/button";
import {Card} from "@/components/ui/card";

interface GameUIData {
    entities: {
        player: {
            uid: string;
        }
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <Card 
            className="w-full h-full aspect-video bg-background flex flex-col items-center justify-between p-8"
            uid={props.data?.entities?.player?.uid || 'main-menu'}
        >
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-foreground tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-12 w-64">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        uid="play-button"
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="w-full"
                    >
                        <Play className="mr-2 h-4 w-4" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        uid="quit-button"
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="w-full"
                    >
                        <Power className="mr-2 h-4 w-4" />
                        Quit
                    </Button>
                )}
            </div>
        </Card>
    );
}
