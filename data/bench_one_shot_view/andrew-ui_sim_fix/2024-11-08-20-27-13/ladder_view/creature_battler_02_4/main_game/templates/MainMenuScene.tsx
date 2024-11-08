import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react';
import {Button} from "@/components/ui/button";

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
        <div 
            className="w-full h-full aspect-video bg-[url('/menu-bg.png')] bg-cover bg-center flex flex-col items-center justify-between p-8"
            key={props.data?.entities?.player?.uid ?? 'main-menu'}
        >
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider drop-shadow-lg">
                    CREATURE BATTLE
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-12 w-64">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-full h-14 text-xl"
                        variant="default"
                    >
                        <Play className="mr-2 h-6 w-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full h-14 text-xl"
                        variant="destructive"
                    >
                        <Power className="mr-2 h-6 w-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
