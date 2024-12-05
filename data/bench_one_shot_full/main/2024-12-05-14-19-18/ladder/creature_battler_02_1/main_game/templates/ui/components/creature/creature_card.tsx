import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
BaseCardTitle = withClickable(BaseCardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <BaseCard uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
          <div className="text-sm">
            HP: {hp}/{maxHp}
          </div>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
