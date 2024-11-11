import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";

interface Player {
    uid: string;
    display_name: string;
}

interface GameUIData {
    entities: {
        player: Player;
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-0 pb-[56.25%] bg-background">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-primary tracking-wider">
                        {props.data?.entities?.player?.display_name || "Game Title"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.includes('play') && (
                        <Button 
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="w-full text-xl"
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
                            className="w-full text-xl"
                        >
                            <XCircle className="w-6 h-6 mr-2" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
