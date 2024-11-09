import {useCurrentButtons} from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Stats {
    [key: string]: number;
}

interface Meta {
    prototype_id?: string;
    category?: string;
    [key: string]: any;
}

interface Skill {
    __type: string;
    stats: {
        base_damage: number;
    };
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

interface Creature {
    __type: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: {
        skills: Skill[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Player {
    __type: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: {
        creatures: Creature[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    __type: string;
    stats: Stats;
    meta: Meta;
    entities: {
        player: Player;
    };
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data?.display_name ?? 'Main Menu'}
                </h1>
            </div>

            <div className="flex-1" />

            <div className="flex-1 flex flex-col items-center justify-center gap-4">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-2 bg-green-600 hover:bg-green-700 px-8 py-6 text-xl"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-2 px-8 py-6 text-xl"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
