import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";

interface GameUIData {
    entities: {
        player: {
            uid: string;
        }
    }
    uid: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const handleButtonClick = (buttonId: string) => {
        emitButtonClick(buttonId);
    };

    return (
        <div className="relative h-screen w-screen flex flex-col bg-background">
            {/* Title Image Section */}
            <div className="flex-1 flex items-center justify-center">
                <div className="w-[600px] h-[200px] bg-muted flex items-center justify-center">
                    {/* Placeholder for title image */}
                    <span className="text-muted-foreground">Game Title Image</span>
                </div>
            </div>

            {/* Button Section */}
            <div className="flex-1 flex flex-col items-center justify-center gap-6">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        uid={`${props.data.uid}-play-btn`}
                        className="w-48 h-12 text-lg flex items-center gap-2"
                        onClick={() => handleButtonClick('play')}
                    >
                        <Play className="w-5 h-5" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        uid={`${props.data.uid}-quit-btn`}
                        variant="destructive"
                        className="w-48 h-12 text-lg flex items-center gap-2"
                        onClick={() => handleButtonClick('quit')}
                    >
                        <XCircle className="w-5 h-5" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
