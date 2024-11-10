import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'
import {Button} from "@/components/ui/button"
import {Card} from "@/components/ui/card"

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
        is_physical: boolean;
    };
}

interface Creature {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, unknown>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, unknown>;
    meta: Record<string, unknown>;
    entities: {
        player: Player;
    };
    collections: Record<string, unknown>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-800 to-slate-900 flex flex-col items-center justify-between p-8 border-0">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data?.display_name || "CREATURE BATTLE"}
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-16">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                        variant="default"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                        variant="destructive"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </Card>
    )
}
