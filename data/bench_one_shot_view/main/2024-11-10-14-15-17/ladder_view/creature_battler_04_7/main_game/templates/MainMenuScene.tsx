import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Player {
    uid: string;
    stats: {
        [key: string]: number;
    };
    meta: {
        [key: string]: any;
    };
    entities: {
        [key: string]: any;
    };
    collections: {
        [key: string]: any[];
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: {
        [key: string]: number;
    };
    meta: {
        [key: string]: any;
    };
    collections: {
        [key: string]: any[];
    };
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
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-12">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-x-2 bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg text-xl font-semibold"
                        size="lg"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-x-2 bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg text-xl font-semibold" 
                        size="lg"
                        variant="destructive"
                    >
                        <Power className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
