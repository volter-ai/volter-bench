import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

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

    if (!props.data) {
        return null;
    }

    return (
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-background">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-primary tracking-wider">
                        GAME TITLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="w-full text-xl py-8"
                        >
                            <Play className="w-6 h-6 mr-2" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            onClick={() => emitButtonClick('quit')}
                            className="w-full text-xl py-8"
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
