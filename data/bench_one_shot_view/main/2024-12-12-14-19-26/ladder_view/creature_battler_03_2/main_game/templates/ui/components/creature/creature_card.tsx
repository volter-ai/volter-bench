import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement>, BaseProps {
  name: string
  currentHp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, currentHp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[250px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`} className="grid gap-4">
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-hp-bar`} value={(currentHp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
